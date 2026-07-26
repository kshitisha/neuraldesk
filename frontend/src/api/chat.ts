import { apiClient } from "./client";

export interface Conversation {
  id: string;
  project_id: string;
  title: string | null;
  created_at: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export const chatApi = {
  createConversation: (projectId: string, title?: string) =>
    apiClient.post<Conversation>(`/projects/${projectId}/conversations`, {
      title,
    }),

  listConversations: (projectId: string) =>
    apiClient.get<Conversation[]>(`/projects/${projectId}/conversations`),

  getMessages: (projectId: string, conversationId: string) =>
    apiClient.get<Message[]>(
      `/projects/${projectId}/conversations/${conversationId}/messages`
    ),
};