from typing import Optional

import matplotlib.pyplot as plt

from labbench_comm.devices.cpar.stimulation_data import StimulationData


def plot_stimulation_data(
    data: StimulationData,
    title: Optional[str] = None,
    show: bool = True,
) -> None:
    """
    Plot CPAR stimulation data.

    Top plot:
        - Pressure (channel 01)
        - Pressure (channel 02)

    Bottom plot:
        - VAS score

    Parameters
    ----------
    data:
        StimulationData instance containing the recorded stimulation samples.
    title:
        Optional figure title.
    show:
        Whether to call plt.show() automatically.
    """

    if not data.has_data:
        raise ValueError("StimulationData contains no samples")

    time = data.time

    fig, (ax_pressure, ax_vas) = plt.subplots(
        nrows=2,
        ncols=1,
        sharex=True,
        figsize=(10, 6),
        constrained_layout=True,
    )

    # ------------------------------------------------------------
    # Pressure plot
    # ------------------------------------------------------------

    ax_pressure.plot(
        time,
        data.actual_pressure_01,
        label="Pressure (1)",  
        color="k",      
        linewidth=1,
    )

    ax_pressure.plot(
        time,
        data.actual_pressure_02,
        label="Pressure (2)",
        color="b",
        linewidth=1,
    )

    ax_pressure.set_ylabel("Pressure [kPa]")
    ax_pressure.set_title("Stimulation Pressure")
    ax_pressure.grid(True)
    ax_pressure.legend(loc="best")

    # ------------------------------------------------------------
    # VAS plot
    # ------------------------------------------------------------

    ax_vas.plot(
        time,
        data.vas_scores,
        label="Rating",
        color="k",
        linewidth=1,
    )

    ax_vas.set_xlabel("Time [s]")
    ax_vas.set_ylabel("Rating [cm]")
    ax_vas.set_title("Visual Analog Rating")
    ax_vas.grid(True)
    ax_vas.legend(loc="best")

    # ------------------------------------------------------------
    # Figure title
    # ------------------------------------------------------------

    if title:
        fig.suptitle(title, fontsize=14)

    if show:
        plt.show()
