import { useEffect, useState } from "react";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProfile() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/profile/");

        if (!response.ok) {
          throw new Error("Profile API error");
        }

        const data = await response.json();
        setProfile(data);
      } catch {
        setError("Не удалось загрузить профиль. Проверь backend.");
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, []);

  if (loading) {
    return <h1>Загрузка профиля...</h1>;
  }

  if (error) {
    return <h1>{error}</h1>;
  }

  return (
    <div style={{ padding: "40px" }}>
      <h1>👤 Профиль</h1>

      <div
        style={{
          marginTop: "24px",
          padding: "24px",
          borderRadius: "18px",
          background: "#1e293b",
          border: "1px solid #334155",
          maxWidth: "500px",
        }}
      >
        <h2>{profile.username}</h2>
        <p>Level: {profile.level}</p>
        <p>XP: {profile.xp}</p>
        <p>Coins: {profile.coins}</p>
      </div>
    </div>
  );
}   