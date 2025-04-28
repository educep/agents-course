"""
BM25 Parameter Visualization

This script generates visualizations to help understand how the BM25 parameters
k1 and b affect the scoring function. It creates multiple plots showing:

1. How k1 affects term frequency saturation (with fixed b)
2. How b affects document length normalization (with fixed k1)
3. Combined effects of both parameters in a heatmap
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# from mpl_toolkits.mplot3d import Axes3D

# Set up a clean, readable plot style
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update(
    {
        "font.size": 12,
        "axes.labelsize": 14,
        "axes.titlesize": 16,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
        "figure.figsize": (10, 6),
        "figure.dpi": 100,
    }
)


def bm25_tf_component(tf, doc_len, avg_doc_len, k1, b):
    """
    Calculate the term frequency component of the BM25 formula.

    Args:
        tf: Term frequency (how many times the term appears in document)
        doc_len: Document length (in tokens)
        avg_doc_len: Average document length across the collection
        k1: Term frequency saturation parameter
        b: Document length normalization parameter

    Returns:
        The BM25 term frequency component score
    """
    # Document length normalization factor
    len_norm = 1 - b + b * (doc_len / avg_doc_len)

    # BM25 term frequency component
    return (k1 + 1) * tf / (k1 * len_norm + tf)


# Part 1: Visualize the effect of k1 on term frequency saturation
def plot_k1_effect():
    """
    Create a plot showing how different k1 values affect term frequency saturation.
    """
    # Term frequency values from 1 to 20
    tf_values = np.arange(1, 21)

    # Various k1 values to demonstrate the effect
    k1_values = [0.0, 0.5, 1.2, 2.0, 5.0, 10.0]

    # Fixed parameters
    b = 0.75
    doc_len = 100
    avg_doc_len = 100

    plt.figure(figsize=(12, 7))

    # Calculate and plot the TF component for each k1 value
    for k1 in k1_values:
        tf_components = [bm25_tf_component(tf, doc_len, avg_doc_len, k1, b) for tf in tf_values]
        plt.plot(
            tf_values, tf_components, marker="o", linewidth=2.5, markersize=8, label=f"k1 = {k1}"
        )

    # Add a linear TF line for comparison with TF-IDF
    plt.plot(
        tf_values,
        tf_values / tf_values.max(),
        "k--",
        linewidth=2,
        label="Normalized Linear TF (TF-IDF)",
    )

    # Add plot details
    plt.xlabel("Term Frequency (occurrences in document)", fontsize=14)
    plt.ylabel("BM25 TF Component Score", fontsize=14)
    plt.title(
        "Effect of k1 on Term Frequency Saturation in BM25\n(b=0.75, document length = average)",
        fontsize=16,
    )
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Annotate key insights
    plt.annotate(
        "k1=0: Full saturation\nafter first occurrence",
        xy=(5, bm25_tf_component(5, doc_len, avg_doc_len, 0, b)),
        xytext=(6, 0.3),
        arrowprops={"arrowstyle": "->"},
        fontsize=12,
    )

    plt.annotate(
        "k1=10: Less saturation,\ncloser to linear TF",
        xy=(15, bm25_tf_component(15, doc_len, avg_doc_len, 10, b)),
        xytext=(12, 2.2),
        arrowprops={"arrowstyle": "->"},
        fontsize=12,
    )

    plt.annotate(
        "Standard range\n(k1=1.2-2.0)",
        xy=(10, bm25_tf_component(10, doc_len, avg_doc_len, 1.5, b)),
        xytext=(7, 1.0),
        arrowprops={"arrowstyle": "->"},
        fontsize=12,
    )

    plt.savefig("bm25_k1_effect.png")


# Part 2: Visualize the effect of b on document length normalization
def plot_b_effect():
    """
    Create a plot showing how different b values affect document length normalization.
    """
    # Document length values relative to average (from 0.1x to 3x the average length)
    rel_doc_lengths = np.linspace(0.1, 3.0, 50)

    # Calculate actual document lengths
    avg_doc_len = 100
    doc_lengths = rel_doc_lengths * avg_doc_len

    # Various b values to demonstrate the effect
    b_values = [0.0, 0.25, 0.5, 0.75, 1.0]

    # Fixed parameters
    k1 = 1.5
    tf = 5  # Fixed term frequency

    plt.figure(figsize=(12, 7))

    # Calculate and plot the TF component for each b value
    for b in b_values:
        tf_components = [
            bm25_tf_component(tf, doc_len, avg_doc_len, k1, b) for doc_len in doc_lengths
        ]
        plt.plot(rel_doc_lengths, tf_components, linewidth=2.5, label=f"b = {b}")

    # Add a constant line for reference (pure TF score without normalization)
    plt.axhline(
        y=bm25_tf_component(tf, avg_doc_len, avg_doc_len, k1, 0),
        color="k",
        linestyle="--",
        linewidth=2,
        label="No Length Normalization Reference",
    )

    # Add vertical line at average document length
    plt.axvline(x=1.0, color="r", linestyle="--", alpha=0.5, label="Average Document Length")

    # Add plot details
    plt.xlabel("Relative Document Length (1.0 = Average Length)", fontsize=14)
    plt.ylabel("BM25 TF Component Score (fixed TF=5)", fontsize=14)
    plt.title(
        "Effect of b on Document Length Normalization in BM25\n(k1=1.5, term frequency=5)",
        fontsize=16,
    )
    plt.legend(loc="upper right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Annotate key insights
    plt.annotate(
        "b=0: No length normalization",
        xy=(2.5, bm25_tf_component(tf, 2.5 * avg_doc_len, avg_doc_len, k1, 0)),
        xytext=(2.0, 2.2),
        arrowprops={"arrowstyle": "->"},
        fontsize=12,
    )

    plt.annotate(
        "b=1.0: Full length normalization\n(score ~ 1/document length)",
        xy=(2.5, bm25_tf_component(tf, 2.5 * avg_doc_len, avg_doc_len, k1, 1.0)),
        xytext=(1.8, 0.7),
        arrowprops={"arrowstyle": "->"},
        fontsize=12,
    )

    plt.annotate(
        "b=0.75: Standard value\n(balanced normalization)",
        xy=(2.0, bm25_tf_component(tf, 2.0 * avg_doc_len, avg_doc_len, k1, 0.75)),
        xytext=(1.3, 1.2),
        arrowprops={"arrowstyle": "->"},
        fontsize=12,
    )

    plt.savefig("bm25_b_effect.png")


# Part 3: Create a 3D visualization showing the combined effect of both parameters
def plot_3d_combined_effect():
    """
    Create a 3D surface plot showing the combined effect of k1 and b parameters.
    """
    # Create a mesh grid for k1 and relative document length
    k1_values = np.linspace(0.5, 3.0, 20)  # Range of k1 values
    rel_doc_lengths = np.linspace(0.5, 2.0, 20)  # Range of relative document lengths

    k1_grid, len_grid = np.meshgrid(k1_values, rel_doc_lengths)

    # Fixed parameters
    avg_doc_len = 100
    tf = 5  # Fixed term frequency

    # Create two separate plots for different b values
    b_values = [0.25, 0.75]

    fig = plt.figure(figsize=(18, 8))

    for i, b in enumerate(b_values):
        # Calculate the TF component for each combination of k1 and document length
        tf_components = np.zeros_like(k1_grid)
        for i_k1 in range(len(k1_values)):
            for i_len in range(len(rel_doc_lengths)):
                k1 = k1_grid[i_len, i_k1]
                doc_len = len_grid[i_len, i_k1] * avg_doc_len
                tf_components[i_len, i_k1] = bm25_tf_component(tf, doc_len, avg_doc_len, k1, b)

        # Create 3D subplot
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        surf = ax.plot_surface(
            k1_grid,
            len_grid,
            tf_components,
            cmap=cm.viridis,
            linewidth=0,
            antialiased=True,
            alpha=0.8,
        )

        # Add plot details
        ax.set_xlabel("k1 Parameter")
        ax.set_ylabel("Relative Doc Length")
        ax.set_zlabel("BM25 TF Component")
        ax.set_title(f"3D Surface: Combined Effect of k1 and Doc Length\n(b={b}, TF=5)")

        # Add a color bar
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

    plt.tight_layout()
    plt.savefig("bm25_3d_combined.png")


# Part 4: Create a heatmap showing how different parameter combinations affect specific documents
def plot_parameter_heatmap():
    """
    Create a heatmap showing how different combinations of k1 and b parameters
    affect BM25 scores for documents of different lengths.
    """
    # Parameter ranges
    k1_values = np.linspace(0.5, 3.0, 20)
    b_values = np.linspace(0.0, 1.0, 20)

    # Document scenarios (each represents a different document length and term frequency)
    scenarios = [
        {"name": "Short doc (TF=2)", "tf": 2, "doc_len": 50, "avg_doc_len": 100},
        {"name": "Average doc (TF=5)", "tf": 5, "doc_len": 100, "avg_doc_len": 100},
        {"name": "Long doc (TF=10)", "tf": 10, "doc_len": 200, "avg_doc_len": 100},
    ]

    # Create a figure with multiple subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for i, scenario in enumerate(scenarios):
        # Calculate scores for each parameter combination
        scores = np.zeros((len(b_values), len(k1_values)))
        for j, b in enumerate(b_values):
            for k, k1 in enumerate(k1_values):
                scores[j, k] = bm25_tf_component(
                    scenario["tf"], scenario["doc_len"], scenario["avg_doc_len"], k1, b
                )

        # Create heatmap
        im = axes[i].imshow(
            scores,
            cmap="viridis",
            aspect="auto",
            origin="lower",
            extent=[min(k1_values), max(k1_values), min(b_values), max(b_values)],
        )

        # Add contour lines for better visualization
        CS = axes[i].contour(
            k1_values, b_values, scores, colors="white", alpha=0.5, linewidths=0.8
        )
        axes[i].clabel(CS, inline=True, fontsize=8, fmt="%.2f")

        # Add plot details
        axes[i].set_xlabel("k1 Parameter")
        axes[i].set_ylabel("b Parameter")
        axes[i].set_title(f'{scenario["name"]}\nTF={scenario["tf"]}, Length={scenario["doc_len"]}')

        # Add color bar
        fig.colorbar(im, ax=axes[i])

        # Mark the standard parameters (k1=1.2-1.5, b=0.75)
        axes[i].plot(1.5, 0.75, "r*", markersize=10)
        axes[i].annotate(
            "Standard\nParameters",
            xy=(1.5, 0.75),
            xytext=(1.7, 0.6),
            arrowprops={"arrowstyle": "->"},
            color="red",
        )

    plt.tight_layout()
    plt.savefig("bm25_parameter_heatmap.png")


# Part 5: Create a plot comparing BM25 scores for different document types as k1 varies
def plot_doc_comparison_k1():
    """
    Create a plot showing how k1 affects the scoring of different document types.
    """
    # k1 values range
    k1_values = np.linspace(0.2, 5.0, 50)

    # Document scenarios
    scenarios = [
        {"name": "Short doc, low TF", "tf": 2, "doc_len": 50, "avg_doc_len": 100, "style": "b-"},
        {"name": "Short doc, high TF", "tf": 5, "doc_len": 50, "avg_doc_len": 100, "style": "b--"},
        {"name": "Long doc, low TF", "tf": 2, "doc_len": 200, "avg_doc_len": 100, "style": "r-"},
        {
            "name": "Long doc, high TF",
            "tf": 10,
            "doc_len": 200,
            "avg_doc_len": 100,
            "style": "r--",
        },
    ]

    # Fixed b parameter
    b = 0.75

    plt.figure(figsize=(12, 7))

    # Calculate and plot scores for each scenario
    for scenario in scenarios:
        scores = [
            bm25_tf_component(scenario["tf"], scenario["doc_len"], scenario["avg_doc_len"], k1, b)
            for k1 in k1_values
        ]

        plt.plot(k1_values, scores, scenario["style"], linewidth=2.5, label=scenario["name"])

    # Add plot details
    plt.xlabel("k1 Parameter", fontsize=14)
    plt.ylabel("BM25 TF Component Score", fontsize=14)
    plt.title("Effect of k1 on Different Document Types\n(fixed b=0.75)", fontsize=16)
    plt.legend(loc="upper right")
    plt.grid(True, alpha=0.3)
    plt.axvline(x=1.5, color="g", linestyle="--", alpha=0.5, label="Typical k1 value")
    plt.tight_layout()

    # Annotate crossing points and insights
    plt.annotate(
        "As k1 increases, high TF\ndocuments gain advantage",
        xy=(3.5, bm25_tf_component(10, 200, 100, 3.5, b)),
        xytext=(3.7, 2.5),
        arrowprops={"arrowstyle": "->"},
        fontsize=12,
    )

    plt.savefig("bm25_k1_doc_comparison.png")


# Part 6: Create a plot comparing BM25 scores for different document types as b varies
def plot_doc_comparison_b():
    """
    Create a plot showing how b affects the scoring of different document types.
    """
    # b values range
    b_values = np.linspace(0.0, 1.0, 50)

    # Document scenarios
    scenarios = [
        {"name": "Short doc, low TF", "tf": 2, "doc_len": 50, "avg_doc_len": 100, "style": "b-"},
        {"name": "Short doc, high TF", "tf": 5, "doc_len": 50, "avg_doc_len": 100, "style": "b--"},
        {"name": "Long doc, low TF", "tf": 2, "doc_len": 200, "avg_doc_len": 100, "style": "r-"},
        {
            "name": "Long doc, high TF",
            "tf": 10,
            "doc_len": 200,
            "avg_doc_len": 100,
            "style": "r--",
        },
    ]

    # Fixed k1 parameter
    k1 = 1.5

    plt.figure(figsize=(12, 7))

    # Calculate and plot scores for each scenario
    for scenario in scenarios:
        scores = [
            bm25_tf_component(scenario["tf"], scenario["doc_len"], scenario["avg_doc_len"], k1, b)
            for b in b_values
        ]

        plt.plot(b_values, scores, scenario["style"], linewidth=2.5, label=scenario["name"])

    # Add plot details
    plt.xlabel("b Parameter", fontsize=14)
    plt.ylabel("BM25 TF Component Score", fontsize=14)
    plt.title("Effect of b on Different Document Types\n(fixed k1=1.5)", fontsize=16)
    plt.legend(loc="upper right")
    plt.grid(True, alpha=0.3)
    plt.axvline(x=0.75, color="g", linestyle="--", alpha=0.5, label="Typical b value")
    plt.tight_layout()

    # Annotate insights
    plt.annotate(
        "b=0: No length normalization\n(scores independent of doc length)",
        xy=(0.05, bm25_tf_component(2, 50, 100, k1, 0.05)),
        xytext=(0.05, 0.9),
        arrowprops={"arrowstyle": "->"},
        fontsize=12,
    )

    plt.annotate(
        "As b increases, shorter docs\ngain advantage over longer docs",
        xy=(0.9, bm25_tf_component(5, 50, 100, k1, 0.9)),
        xytext=(0.5, 2.2),
        arrowprops={"arrowstyle": "->"},
        fontsize=12,
    )

    plt.savefig("bm25_b_doc_comparison.png")


if __name__ == "__main__":
    print("Generating BM25 parameter visualization plots...")

    # Generate all plots
    plot_k1_effect()
    plot_b_effect()
    plot_3d_combined_effect()
    plot_parameter_heatmap()
    plot_doc_comparison_k1()
    plot_doc_comparison_b()

    print("Done! The following visualization files have been created:")
    print("- bm25_k1_effect.png: Effect of k1 on term frequency saturation")
    print("- bm25_b_effect.png: Effect of b on document length normalization")
    print("- bm25_3d_combined.png: 3D visualization of combined parameter effects")
    print("- bm25_parameter_heatmap.png: Heatmap of parameter combinations")
    print("- bm25_k1_doc_comparison.png: How k1 affects different document types")
    print("- bm25_b_doc_comparison.png: How b affects different document types")
