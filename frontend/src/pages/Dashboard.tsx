import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { projectsApi, type Project, type ProjectCreate } from "../api/projects";
import { useAuthStore } from "../store/authStore";

const MODELS_BY_PROVIDER: Record<string, string[]> = {
  openai: ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
  openrouter: ["openai/gpt-4o", "mistralai/mixtral-8x7b", "anthropic/claude-3-haiku"],
  groq: ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
};

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [form, setForm] = useState<ProjectCreate>({
    name: "",
    description: "",
    system_prompt: "",
    model: "gpt-4o",
    temperature: 0.7,
    provider: "openai",
  });

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const res = await projectsApi.list();
      setProjects(res.data);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setForm({ name: "", description: "", system_prompt: "", model: "gpt-4o", temperature: 0.7, provider: "openai" });
    setEditingProject(null);
    setShowForm(false);
  };

  const handleProviderChange = (provider: string) => {
    const defaultModel = MODELS_BY_PROVIDER[provider]?.[0] || "";
    setForm({ ...form, provider, model: defaultModel });
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await projectsApi.create(form);
      setProjects([res.data, ...projects]);
      resetForm();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to create project.");
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingProject) return;
    try {
      const res = await projectsApi.update(editingProject.id, form);
      setProjects(projects.map((p) => (p.id === editingProject.id ? res.data : p)));
      resetForm();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to update project.");
    }
  };

  const handleEdit = (project: Project) => {
    setEditingProject(project);
    setForm({
      name: project.name,
      description: project.description || "",
      system_prompt: project.system_prompt || "",
      model: project.model,
      temperature: project.temperature,
      provider: project.provider,
    });
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this project?")) return;
    try {
      await projectsApi.delete(id);
      setProjects(projects.filter((p) => p.id !== id));
    } catch {}
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <header className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold text-white">NeuralDesk</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-400">{user?.email}</span>
          <button
            onClick={() => { logout(); navigate("/login"); }}
            className="text-sm text-gray-400 hover:text-white transition"
          >
            Sign out
          </button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold">Projects</h2>
            <p className="text-gray-400 text-sm mt-1">Each project is an AI agent with its own configuration.</p>
          </div>
          <button
            onClick={() => { resetForm(); setShowForm(!showForm); }}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition"
          >
            + New Project
          </button>
        </div>

        
        {showForm && (
          <form
            onSubmit={editingProject ? handleUpdate : handleCreate}
            className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-8 space-y-4"
          >
            <h3 className="font-semibold text-white">
              {editingProject ? `Editing: ${editingProject.name}` : "New Project"}
            </h3>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-gray-400 mb-1 block">Name *</label>
                <input
                  required
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500"
                  placeholder="My Assistant"
                />
              </div>
              <div>
                <label className="text-xs text-gray-400 mb-1 block">Provider</label>
                <select
                  value={form.provider}
                  onChange={(e) => handleProviderChange(e.target.value)}
                  className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="openai">OpenAI</option>
                  <option value="openrouter">OpenRouter</option>
                  <option value="groq">Groq</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-gray-400 mb-1 block">Description</label>
                <input
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500"
                  placeholder="What does this agent do?"
                />
              </div>
              <div>
                <label className="text-xs text-gray-400 mb-1 block">Model</label>
                <select
                  value={form.model}
                  onChange={(e) => setForm({ ...form, model: e.target.value })}
                  className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500"
                >
                  {(MODELS_BY_PROVIDER[form.provider as keyof typeof MODELS_BY_PROVIDER] ?? []).map(
  (model) => (
    <option key={model} value={model}>
      {model}
    </option>
  )
)}
                </select>
              </div>
            </div>

            <div>
              <label className="text-xs text-gray-400 mb-1 block">System Prompt</label>
              <textarea
                value={form.system_prompt}
                onChange={(e) => setForm({ ...form, system_prompt: e.target.value })}
                rows={3}
                className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500 resize-none"
                placeholder="You are a helpful assistant..."
              />
            </div>

            <div>
              <label className="text-xs text-gray-400 mb-1 block">
                Temperature: {form.temperature}
              </label>
              <input
                type="range"
                min={0}
                max={2}
                step={0.1}
                value={form.temperature}
                onChange={(e) => setForm({ ...form, temperature: parseFloat(e.target.value) })}
                className="w-full accent-indigo-500"
              />
            </div>

            <div className="flex gap-3 pt-2">
              <button
                type="submit"
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition"
              >
                {editingProject ? "Save Changes" : "Create Project"}
              </button>
              <button
                type="button"
                onClick={resetForm}
                className="text-gray-400 hover:text-white px-4 py-2 text-sm transition"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        
        {loading ? (
          <p className="text-gray-500 text-sm">Loading projects...</p>
        ) : projects.length === 0 ? (
          <div className="text-center py-20 text-gray-600">
            <p className="text-lg">No projects yet.</p>
            <p className="text-sm mt-1">Create your first AI agent above.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {projects.map((project) => (
              <div
                key={project.id}
                className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-white">{project.name}</h3>
                    <p className="text-xs text-gray-500 mt-0.5">
                      {project.model} · {project.provider}
                    </p>
                  </div>
                  <div className="flex gap-3">
                    <button
                      onClick={() => handleEdit(project)}
                      className="text-gray-500 hover:text-indigo-400 text-xs transition"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(project.id)}
                      className="text-gray-500 hover:text-red-400 text-xs transition"
                    >
                      Delete
                    </button>
                  </div>
                </div>

                {project.description && (
                  <p className="text-sm text-gray-400 mb-4">{project.description}</p>
                )}

                <button
                  onClick={() => navigate(`/chat/${project.id}`)}
                  className="w-full bg-gray-800 hover:bg-gray-700 text-white text-sm py-2 rounded-lg transition"
                >
                  Open Chat →
                </button>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}