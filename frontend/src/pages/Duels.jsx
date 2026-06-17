import "./Duels.css";

const duelModes = [
  {
    title: "Quick Match",
    text: "Fast 1v1 quiz battles for daily practice.",
    status: "Coming soon",
  },
  {
    title: "Ranked Duel",
    text: "Competitive learning ladder with rating rewards.",
    status: "API planned",
  },
  {
    title: "Boss Challenge",
    text: "Team up against difficult subject bosses.",
    status: "Quiz integration required",
  },
];

export default function Duels() {
  return (
    <main className="duels-page">
      <section className="duels-shell">
        <header className="duels-hero">
          <div>
            <span className="duels-eyebrow">Planned module</span>
            <h1>Duels Arena</h1>
            <p>Battle-based learning mode</p>
          </div>

          <div className="duels-stats">
            <div>
              <span>Wins</span>
              <strong>0</strong>
            </div>
            <div>
              <span>Rating</span>
              <strong>1000</strong>
            </div>
            <div>
              <span>Battle XP</span>
              <strong>0</strong>
            </div>
          </div>
        </header>

        <article className="duels-feature-card">
          <span className="duels-badge">PvP learning</span>
          <h2>Answer quiz questions in 1v1 battles</h2>
          <p>
            Duels will let students challenge each other, answer subject questions,
            earn battle XP, and climb a ranked learning ladder.
          </p>
        </article>

        <section className="duel-mode-grid">
          {duelModes.map((mode) => (
            <article className="duel-mode-card" key={mode.title}>
              <span>{mode.status}</span>
              <h3>{mode.title}</h3>
              <p>{mode.text}</p>
              <button disabled>Locked</button>
            </article>
          ))}
        </section>
      </section>
    </main>
  );
}
