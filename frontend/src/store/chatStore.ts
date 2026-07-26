import { create } from "zustand";
import type { Message } from "../api/chat";

interface ChatState {
  messages: Message[];
  streamingContent: string;
  isStreaming: boolean;
  activeConversationId: string | null;
  setConversation: (id: string) => void;
  setMessages: (messages: Message[]) => void;
  addMessage: (message: Message) => void;
  appendChunk: (chunk: string) => void;
  finalizeStream: () => void;
  setStreaming: (value: boolean) => void;
  clearChat: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  streamingContent: "",
  isStreaming: false,
  activeConversationId: null,

  setConversation: (id) =>
    set({ activeConversationId: id, messages: [], streamingContent: "" }),

  setMessages: (messages) => set({ messages }),

  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),

  appendChunk: (chunk) =>
    set((state) => ({ streamingContent: state.streamingContent + chunk })),

  finalizeStream: () => {
    const { streamingContent, messages } = get();
    if (!streamingContent) return;
    const assistantMessage: Message = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: streamingContent,
      created_at: new Date().toISOString(),
    };
    set({ messages: [...messages, assistantMessage], streamingContent: "", isStreaming: false });
  },

  setStreaming: (value) => set({ isStreaming: value }),

  clearChat: () =>
    set({ messages: [], streamingContent: "", activeConversationId: null }),
}));