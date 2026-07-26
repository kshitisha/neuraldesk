import { apiClient } from "./client";

export interface Project {
  id: string;
  name: string;
  description: string | null;
  system_prompt: string | null;
  model: string;
  temperature: number;
  provider: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  system_prompt?: string;
  model?: string;
  temperature?: number;
  provider?: string;
}

export interface Prompt {
  id: string;
  title: string;
  content: string;
  created_at: string;
}

export const projectsApi = {
  list: () => apiClient.get<Project[]>("/projects"),

  create: (data: ProjectCreate) =>
    apiClient.post<Project>("/projects", data),

  get: (id: string) => apiClient.get<Project>(`/projects/${id}`),

  update: (id: string, data: Partial<ProjectCreate>) =>
    apiClient.put<Project>(`/projects/${id}`, data),

  delete: (id: string) => apiClient.delete(`/projects/${id}`),

  getPrompts: (projectId: string) =>
    apiClient.get<Prompt[]>(`/projects/${projectId}/prompts`),

  addPrompt: (projectId: string, title: string, content: string) =>
    apiClient.post<Prompt>(`/projects/${projectId}/prompts`, { title, content }),

  deletePrompt: (projectId: string, promptId: string) =>
    apiClient.delete(`/projects/${projectId}/prompts/${promptId}`),
};