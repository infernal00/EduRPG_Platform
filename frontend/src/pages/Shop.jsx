import "./Shop.css";

const shopItems = [
  {
    title: "XP Booster",
    text: "Increase lesson rewards for a short learning session.",
    price: 50,
  },
  {
    title: "Streak Shield",
    text: "Protect a daily streak when life gets busy.",
    price: 75,
  },
  {
    title: "Avatar Frame",
    text: "Unlock a glowing cosmetic profile border.",
    price: 120,
  },
  {
    title: "Hint Token",
    text: "Use one hint during a difficult quiz battle.",
    price: 25,
  },
];

export default function Shop() {
  return (
    <main className="shop-page">
      <section className="shop-shell">
        <header className="shop-hero">
          <div>
            <span className="shop-eyebrow">Planned module</span>
            <h1>Arcane Shop</h1>
            <p>Spend coins on learning boosts and cosmetics</p>
          </div>

          <div className="coin-card">
            <span>Current coins</span>
            <strong>15</strong>
            <p>Fallback wallet for demo</p>
          </div>
        </header>

        <section className="shop-grid">
          {shopItems.map((item) => (
            <article className="shop-item-card" key={item.title}>
              <span className="item-status">Coming soon</span>
              <h2>{item.title}</h2>
              <p>{item.text}</p>
              <div className="item-footer">
                <strong>{item.price} coins</strong>
                <button disabled>Buy later</button>
              </div>
            </article>
          ))}
        </section>
      </section>
    </main>
  );
}
