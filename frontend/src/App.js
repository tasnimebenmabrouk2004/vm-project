import { useEffect, useState } from "react";
import axios from "axios";
import './App.css';

const API_KEY = "key1234567";
const BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [vms, setVms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ name: "", os: "", cpu: "", ram: "" });
  const [error, setError] = useState("");

  const fetchVMs = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${BASE_URL}/vms/`, {
        headers: { "X-API-Key": API_KEY },
      });
      setVms(res.data);
      setError("");
    } catch {
      setError("⚠️ Failed to fetch VMs");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchVMs();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!form.name || !form.os || !form.cpu || !form.ram) {
      setError("Please fill all fields.");
      return;
    }

    try {
      await axios.post(
        `${BASE_URL}/vms/`,
        {
          name: form.name,
          os: form.os,
          cpu: parseInt(form.cpu),
          ram: parseInt(form.ram),
        },
        {
          headers: { "X-API-Key": API_KEY },
        }
      );
      setForm({ name: "", os: "", cpu: "", ram: "" });
      fetchVMs();
      setError("");
    } catch {
      setError("⚠️ Failed to create VM");
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${BASE_URL}/vms/${id}`, {
        headers: { "X-API-Key": API_KEY },
      });
      fetchVMs();
      setError("");
    } catch {
      setError("⚠️ Failed to delete VM");
    }
  };

  const handleToggle = async (id) => {
    try {
      await axios.patch(`${BASE_URL}/vms/${id}/toggle_status`, null, {
        headers: { "X-API-Key": API_KEY },
      });
      fetchVMs();
      setError("");
    } catch {
      setError("⚠️ Failed to toggle status");
    }
  };

  return (
    <div className="container">
      <h1> VM Dashboard</h1>

      <form onSubmit={handleCreate} style={{ marginBottom: "2rem" }}>
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
          style={{ marginRight: "1rem", padding: "0.5rem", borderRadius: "6px" }}
        />
        <input
          type="text"
          name="os"
          placeholder="Operating System"
          value={form.os}
          onChange={handleChange}
          style={{ marginRight: "1rem", padding: "0.5rem", borderRadius: "6px" }}
        />
        <input
          type="number"
          name="cpu"
          placeholder="CPU"
          value={form.cpu}
          onChange={handleChange}
          style={{ marginRight: "1rem", padding: "0.5rem", borderRadius: "6px" }}
        />
        <input
          type="number"
          name="ram"
          placeholder="RAM"
          value={form.ram}
          onChange={handleChange}
          style={{ marginRight: "1rem", padding: "0.5rem", borderRadius: "6px" }}
        />
        <button type="submit" className="toggle">
          Create
        </button>
      </form>

      {error && <p style={{ color: "red", marginBottom: "1rem" }}>{error}</p>}

      {loading ? (
        <p>Loading VMs...</p>
      ) : (
        vms.map((vm) => (
          <div key={vm.id} className="vm-card">
            <h3>{vm.name}</h3>
            <p>
              {vm.os} | {vm.cpu} CPU | {vm.ram} GB RAM
            </p>
            <p>
              Status:{" "}
              <span style={{ fontWeight: "600", color: vm.status === "running" ? "#38a169" : "#e53e3e" }}>
                {vm.status}
              </span>
            </p>
            <div>
              <button className="toggle" onClick={() => handleToggle(vm.id)}>
                Toggle Status
              </button>
              <button className="delete" onClick={() => handleDelete(vm.id)}>
                Delete
              </button>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default App;
