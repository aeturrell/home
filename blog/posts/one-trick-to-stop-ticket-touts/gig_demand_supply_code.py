import matplotlib.pyplot as plt
import numpy as np

plt.style.use("plot_style.txt")

colors_from_style = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# Set up the figure
fig, ax = plt.subplots(figsize=(8, 4))

# Define quantity range
q = np.linspace(0, 10, 100)

# Define demand curve (downward sloping)
demand = 100 - 8 * q

# Define supply curve (vertical - fixed capacity venue)
venue_capacity = 5
supply_q = np.array([venue_capacity, venue_capacity])
supply_p = np.array([0, 120])

# Define prices
p_artist = 40  # Artist's preferred/face value price
p_equilibrium = 100 - 8 * venue_capacity  # Equilibrium/resale price

# Plot demand curve
ax.plot(q, demand, "b-", linewidth=2.5, label="Demand")

# Plot supply curve (vertical line at venue capacity)
ax.plot(supply_q, supply_p, "r-", linewidth=2.5, label="Supply (venue capacity)")

# Mark the equilibrium point
ax.plot(venue_capacity, p_equilibrium, "ko", markersize=10, zorder=5)

# Draw horizontal lines for prices
ax.axhline(y=p_artist, color="green", linestyle="--", linewidth=1.5, alpha=0.7)
ax.axhline(y=p_equilibrium, color="purple", linestyle="--", linewidth=1.5, alpha=0.7)

# Shade the consumer surplus area
# This is the area between demand curve and artist's price, up to venue capacity
q_surplus = np.linspace(0, venue_capacity, 100)
demand_surplus = 100 - 8 * q_surplus
ax.fill_between(
    q_surplus,
    p_artist,
    p_equilibrium,
    alpha=0.3,
    color=colors_from_style[0],
    label="Consumer Surplus",
)

# Add labels for prices
ax.text(
    -0.5,
    p_artist,
    "p (face value)",
    fontsize=12,
    verticalalignment="bottom",
    fontweight="bold",
    color="green",
)
ax.text(
    -0.5,
    p_equilibrium,
    "p' (equilibrium/resale)",
    fontsize=12,
    verticalalignment="bottom",
    fontweight="bold",
    color="purple",
)

# Add label for equilibrium point
ax.text(
    venue_capacity + 0.2,
    p_equilibrium + 3,
    "Equilibrium",
    fontsize=11,
    fontweight="bold",
)

# Add annotation for consumer surplus
ax.annotate(
    "Artist-gifted fan surplus (when p < p')",
    xy=(4, ((p_equilibrium + p_artist) / 2)),
    fontsize=9,
    ha="right",
    va="bottom",
    fontweight="bold",
)

# Add vertical line at venue capacity
ax.axvline(x=venue_capacity, color="gray", linestyle=":", alpha=0.5)
ax.text(
    venue_capacity+0.1,
    4,
    "Q* (venue capacity)",
    fontsize=11,
    ha="left",
    fontweight="bold",
)

# Labels and title
ax.set_xlabel("Quantity of Tickets (10,000s)", fontsize=12, fontweight="bold")
ax.set_ylabel("Price (£)", fontsize=12, fontweight="bold")
ax.set_title(
    "Market for Gig Tickets",
    fontsize=14,
    fontweight="bold",
)

ax.annotate(
    "Demand",
    xy=(8, 35),
    xytext=(8, 20),
    arrowprops=dict(facecolor="black", arrowstyle="->"),
    fontsize=11,
    fontweight="bold",
)

ax.annotate(
    "Supply",
    xy=(5, 70),
    xytext=(7, 90),
    arrowprops=dict(facecolor="black", arrowstyle="->"),
    fontsize=11,
    fontweight="bold",
)

# Set axis limits
ax.set_xlim(-1, 10)
ax.set_ylim(0, 110)

# Add grid
ax.grid(True, alpha=0.3, linestyle="-", linewidth=0.5)

plt.tight_layout()
plt.savefig("blog/posts/one-trick-to-stop-ticket-touts/gig_demand_supply.svg", bbox_inches='tight')
