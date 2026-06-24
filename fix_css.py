with open('frontend/src/App.css', 'w', encoding='utf-8') as f:
    f.write("""
/* ===== RESET & BASE ===== */
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0a0a1a;
  color: #e2e8f0;
  font-family: 'Segoe UI', system-ui, sans-serif;
  min-height: 100vh;
}

/* ===== NAVBAR ===== */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  height: 64px;
  background: rgba(10, 10, 30, 0.95);
  border-bottom: 1px solid rgba(139, 92, 246, 0.3);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
}
.navbar h2 {
  font-size: 1.4rem;
  font-weight: 800;
  background: linear-gradient(135deg, #a78bfa, #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 1px;
}
.navbar div { display: flex; align-items: center; gap: 0.25rem; }
.navbar a {
  color: #94a3b8;
  text-decoration: none;
  padding: 0.5rem 0.9rem;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.2s;
}
.navbar a:hover { color: #a78bfa; background: rgba(139, 92, 246, 0.1); }
.btn-logout {
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.4);
  color: #94a3b8;
  padding: 0.4rem 0.9rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  margin-left: 0.5rem;
  transition: all 0.2s;
}
.btn-logout:hover { border-color: #f87171; color: #f87171; }

/* ===== AUTH PAGES ===== */
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(ellipse at top, #1e1b4b 0%, #0a0a1a 70%);
}
.auth-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 20px;
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  backdrop-filter: blur(20px);
  box-shadow: 0 25px 50px rgba(0,0,0,0.5), 0 0 80px rgba(139,92,246,0.1);
}
.auth-card h1 {
  font-size: 2rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #a78bfa, #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.auth-card > .muted { text-align: center; margin-bottom: 1.5rem; }
.field { display: flex; flex-direction: column; gap: 6px; margin-bottom: 1rem; }
.field label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
.field input {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 10px;
  padding: 0.7rem 1rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.field input:focus {
  border-color: #a78bfa;
  box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.1);
}

/* ===== PAGES ===== */
.page {
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}
.page h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #a78bfa, #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.page h2 {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 2rem 0 1rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.page-loading {
  padding: 4rem;
  text-align: center;
  color: #6366f1;
  font-size: 1.1rem;
}
.muted { color: #64748b; font-size: 0.9rem; }
.error-box {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
.toast {
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #86efac;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
}

/* ===== STATS GRID ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  margin-bottom: 1.5rem;
}
.stat-card {
  background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(96,165,250,0.05));
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 14px;
  padding: 1.25rem 1rem;
  text-align: center;
  transition: transform 0.2s, border-color 0.2s;
}
.stat-card:hover { transform: translateY(-2px); border-color: rgba(139,92,246,0.5); }
.stat-label {
  display: block;
  font-size: 0.7rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 6px;
}
.stat-value { display: block; font-size: 1.6rem; font-weight: 700; color: #e2e8f0; }

/* ===== XP BAR ===== */
.xp-bar-wrap { margin-bottom: 2rem; }
.xp-bar-label { font-size: 0.82rem; color: #64748b; margin-bottom: 8px; }
.xp-bar {
  background: rgba(255,255,255,0.05);
  border-radius: 999px;
  height: 8px;
  overflow: hidden;
  border: 1px solid rgba(139,92,246,0.1);
}
.xp-bar-fill {
  background: linear-gradient(90deg, #7c3aed, #a78bfa, #60a5fa);
  height: 100%;
  border-radius: 999px;
  transition: width 0.8s ease;
  box-shadow: 0 0 10px rgba(167,139,250,0.5);
}

/* ===== CARDS ===== */
.lessons-list, .duels-list { display: grid; gap: 12px; }
.lesson-card, .duel-card {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  transition: border-color 0.2s, transform 0.2s;
}
.lesson-card:hover, .duel-card:hover {
  border-color: rgba(139,92,246,0.4);
  transform: translateX(4px);
}
.lesson-card h3 { margin-bottom: 0.5rem; font-size: 1rem; color: #e2e8f0; }
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.75rem;
}

/* ===== PROFILE ===== */
.profile-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 2rem;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(139,92,246,0.2);
  border-radius: 16px;
  padding: 1.5rem;
}
.avatar {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #7c3aed, #2563eb);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: 800;
  flex-shrink: 0;
  box-shadow: 0 0 20px rgba(124,58,237,0.4);
}
.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
}
.achievement-card {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(139,92,246,0.2);
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  transition: border-color 0.2s;
}
.achievement-card:hover { border-color: rgba(251,191,36,0.5); }
.ach-icon { font-size: 2rem; display: block; margin-bottom: 6px; }
.ach-name { font-size: 0.78rem; color: #94a3b8; }

/* ===== MAP ===== */
.map-page { padding: 2rem; max-width: 1000px; margin: 0 auto; }
.map-page h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #a78bfa, #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.map-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}
.location-card {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(139,92,246,0.2);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}
.location-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, #7c3aed, #60a5fa);
  opacity: 0;
  transition: opacity 0.3s;
}
.location-card:hover { border-color: rgba(139,92,246,0.5); transform: translateY(-4px); box-shadow: 0 10px 30px rgba(124,58,237,0.15); }
.location-card:hover::before { opacity: 1; }
.location-card.completed { border-color: rgba(34,197,94,0.3); }
.location-card h3 { margin-bottom: 0.5rem; font-size: 1rem; }
.location-card p { font-size: 0.85rem; color: #64748b; margin-bottom: 1rem; }
.done-badge { font-size: 0.75rem; color: #86efac; display: block; margin-bottom: 6px; }
.location-card button {
  background: linear-gradient(135deg, #7c3aed, #2563eb);
  color: #fff;
  border: none;
  padding: 0.45rem 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: opacity 0.2s, transform 0.2s;
}
.location-card button:hover { opacity: 0.85; transform: scale(1.03); }

/* ===== SHOP ===== */
.shop-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 14px;
}
.shop-card {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(139,92,246,0.15);
  border-radius: 14px;
  padding: 1.25rem;
  transition: border-color 0.2s, transform 0.2s;
}
.shop-card:hover { border-color: rgba(251,191,36,0.4); transform: translateY(-2px); }
.shop-card h3 { margin-bottom: 0.4rem; font-size: 1rem; }
.shop-card .btn-primary { margin-top: 0.75rem; }

/* ===== DUELS ===== */
.duel-players { display: flex; align-items: center; gap: 1rem; font-weight: 600; }
.vs { color: #475569; font-size: 0.8rem; padding: 0.2rem 0.5rem; background: rgba(255,255,255,0.05); border-radius: 6px; }
.duel-meta { display: flex; gap: 8px; margin-top: 10px; }

/* ===== BADGES & BUTTONS ===== */
.badge {
  background: rgba(124, 58, 237, 0.2);
  color: #a78bfa;
  font-size: 0.75rem;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid rgba(167,139,250,0.2);
  font-weight: 500;
}
.badge-gold {
  background: rgba(251, 191, 36, 0.1);
  color: #fbbf24;
  border-color: rgba(251,191,36,0.2);
}
.btn-primary {
  background: linear-gradient(135deg, #7c3aed, #2563eb);
  color: #fff;
  border: none;
  padding: 0.7rem 1.4rem;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  width: 100%;
  display: block;
  transition: opacity 0.2s, transform 0.2s;
  letter-spacing: 0.3px;
}
.btn-primary:hover { opacity: 0.88; transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
""")
print('OK')
