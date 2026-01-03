"""
This module generates raw (bronze-layer) datasets for the
Navigator Auto Journey analytics project.

It produces deterministic, realistic synthetic data for:
- raw_customers
- raw_vehicles
- raw_events

The generation logic follows the assumptions and definitions
documented in /docs and is intended to support analytics
development, experimentation, and data quality validation.
"""

# High-level flow:
# 1. Set random seed for determinism
# 2. Generate raw_customers based on documented assumptions
# 3. Generate raw_vehicles using external dataset distributions
# 4. Generate raw_events to simulate browsing-to-purchase journeys
# 5. Write outputs to data/raw/ as parquet files

import random
import numpy as np

# Configuration
RANDOM_SEED = 42
DEFAULT_CUSTOMER_COUNT = 50_000


def set_seed(seed: int = RANDOM_SEED) -> None:
    """
    Sets random seeds for reproducible data generation.
    """
    random.seed(seed)
    np.random.seed(seed)
