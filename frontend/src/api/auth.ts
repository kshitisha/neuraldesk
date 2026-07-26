import { apiClient } from "./client";

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
}

export const authApi = {
  register: (data: RegisterData) =>
    apiClient.post<User>("/auth/register", data),

  login: (data: LoginData) =>
    apiClient.post<TokenResponse>("/auth/login", data),

  me: () => apiClient.get<User>("/auth/me"),
};