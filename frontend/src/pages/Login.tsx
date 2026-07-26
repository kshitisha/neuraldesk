import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authApi } from "../api/auth";
import { useAuthStore } from "../store/authStore";

export default function Login() {
  const navigate = useNavigate();
  const { setAuth } = useAuthStore();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const tokenRes = await authApi.login(form);
      const { access_token, refresh_token } = tokenRes.data;
      localStorage.setItem("access_token", access_token);
      const userRes = await authApi.me();
      setAuth(userRes.data, access_token, refresh_token);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-white">NeuralDesk</h1>
          <p className="text-gray-400 mt-2">Sign in to your account</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="bg-gray-900 border border-gray-800 rounded-xl p-8 space-y-5"
        >
          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-sm px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm text-gray-400 mb-1">Email</label>
            <input
              type="email"
              required
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-2.5 focus:outline-none focus:border-indigo-500"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Password</label>
            <input
              type="password"
              required
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-2.5 focus:outline-none focus:border-indigo-500"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition"
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>

          <p className="text-center text-sm text-gray-500">
            Don't have an account?{" "}
            <Link to="/register" className="text-indigo-400 hover:underline">
              Register
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}