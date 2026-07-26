import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { chatApi, type Conversation, type Message } from "../api/chat";
import { projectsApi, type Project, type Prompt } from "../api/projects";
import { useChatStore } from "../store/chatStore";

export default function ChatPage() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const {
    messages,
    streamingContent,
    isStreaming,
    activeConversationId,
    setConversation,
    setMessages,
    addMessage,
    appendChunk,
    finalizeStream,
    setStreaming,
  } = useChatStore();

  const [project, setProject] = useState<Project | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [input, setInput] = useState("");
  const [showPrompts, setShowPrompts] = useState(false);

  useEffect(() => {
    if (projectId) loadProject();
  }, [projectId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingContent]);

  const loadProject = async () => {
    try {
      const [projRes, convRes, promptRes] = await Promise.all([
        projectsApi.get(projectId!),
        chatApi.listConversations(projectId!),
        projectsApi.getPrompts(projectId!),
      ]);
      setProject(projRes.data);
      setConversations(convRes.data);
      setPrompts(promptRes.data);

      if (convRes.data.length > 0) {
        await selectConversation(convRes.data[0]);
      }
    } catch {
      navigate("/dashboard");
    }
  };

  const selectConversation = async (conv: Conversation) => {
    setConversation(conv.id);
    const res = await chatApi.getMessages(projectId!, conv.id);
    setMessages(res.data);
  };

  const createConversation = async () => {
    const res = await chatApi.createConversation(projectId!, "New Conversation");
    const newConv = res.data;
    setConversations([newConv, ...conversations]);
    setConversation(newConv.id);
    setMessages([]);
  };

  const sendMessage = async () => {
    if (!input.trim() || isStreaming || !activeConversationId) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: input.trim(),
      created_at: new Date().toISOString(),
    };

    addMessage(userMessage);
    const messageText = input.trim();
    setInput("");
    setStreaming(true);

    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch(
  `https://neuraldesk-production.up.railway.app/api/v1/projects/${projectId}/conversations/${activeConversationId}/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ message: messageText }),
        }
      );

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        const lines = chunk.split("\n").filter((l) => l.startsWith("data: "));
        for (const line of lines) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.content) appendChunk(data.content);
            if (data.done) finalizeStream();
            if (data.error) {
              setStreaming(false);
              alert("AI error: " + data.error);
            }
          } catch {}
        }
      }
      finalizeStream();
    } catch {
      setStreaming(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const injectPrompt = (content: string) => {
    setInput(content);
    setShowPrompts(false);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col">
      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate("/dashboard")}
            className="text-gray-400 hover:text-white text-sm transition"
          >
            ← Back
          </button>
          <div>
            <h1 className="font-semibold text-white">{project?.name}</h1>
            <p className="text-xs text-gray-500">{project?.model} · {project?.provider}</p>
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-60 border-r border-gray-800 flex flex-col shrink-0">
          <div className="p-4 border-b border-gray-800">
            <button
              onClick={createConversation}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-sm py-2 rounded-lg transition"
            >
              + New Chat
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => selectConversation(conv)}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm transition ${
                  activeConversationId === conv.id
                    ? "bg-gray-800 text-white"
                    : "text-gray-400 hover:bg-gray-800/50 hover:text-white"
                }`}
              >
                {conv.title || "Conversation"}
              </button>
            ))}
          </div>
        </aside>

        {/* Chat Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4">
            {messages.length === 0 && !isStreaming && (
              <div className="text-center text-gray-600 mt-20">
                <p className="text-lg">Start a conversation</p>
                <p className="text-sm mt-1">
                  {project?.system_prompt
                    ? `Agent: "${project.system_prompt.slice(0, 60)}..."`
                    : "No system prompt configured."}
                </p>
              </div>
            )}

            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-2xl px-4 py-3 rounded-xl text-sm whitespace-pre-wrap ${
                    msg.role === "user"
                      ? "bg-indigo-600 text-white"
                      : "bg-gray-800 text-gray-100"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}

            {/* Streaming bubble */}
            {isStreaming && streamingContent && (
              <div className="flex justify-start">
                <div className="max-w-2xl px-4 py-3 rounded-xl text-sm bg-gray-800 text-gray-100 whitespace-pre-wrap">
                  {streamingContent}
                  <span className="inline-block w-1.5 h-4 bg-indigo-400 ml-1 animate-pulse" />
                </div>
              </div>
            )}

            {isStreaming && !streamingContent && (
              <div className="flex justify-start">
                <div className="px-4 py-3 rounded-xl bg-gray-800 text-gray-400 text-sm">
                  Thinking...
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-800 px-6 py-4 shrink-0">
            {/* Prompt Library */}
            {showPrompts && prompts.length > 0 && (
              <div className="mb-3 bg-gray-900 border border-gray-700 rounded-xl p-3 space-y-2 max-h-48 overflow-y-auto">
                <p className="text-xs text-gray-500 font-medium">Prompt Library</p>
                {prompts.map((p) => (
                  <button
                    key={p.id}
                    onClick={() => injectPrompt(p.content)}
                    className="w-full text-left px-3 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition"
                  >
                    <p className="text-sm text-white font-medium">{p.title}</p>
                    <p className="text-xs text-gray-400 truncate">{p.content}</p>
                  </button>
                ))}
              </div>
            )}

            <div className="flex items-end gap-3">
              {prompts.length > 0 && (
                <button
                  onClick={() => setShowPrompts(!showPrompts)}
                  className="text-gray-500 hover:text-indigo-400 text-xs transition pb-2"
                  title="Prompt Library"
                >
                  ⚡
                </button>
              )}

              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isStreaming || !activeConversationId}
                rows={1}
                className="flex-1 bg-gray-800 border border-gray-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 resize-none disabled:opacity-50"
                placeholder={
                  !activeConversationId
                    ? "Create a conversation to start chatting"
                    : "Message... (Enter to send, Shift+Enter for new line)"
                }
              />

              <button
                onClick={sendMessage}
                disabled={isStreaming || !input.trim() || !activeConversationId}
                className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 text-white px-4 py-3 rounded-xl text-sm font-medium transition"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}