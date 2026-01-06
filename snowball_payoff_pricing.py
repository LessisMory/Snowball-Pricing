# ============================================================
# Snowball Product: Observation Schedule and KO Barrier Design
# ============================================================
# This section defines the observation dates and corresponding
# knock-out (KO) barrier levels for the Snowball structured product.
# Observation dates are typically monthly and determine whether
# the product is early redeemed.

# Define observation dates using trading-day approximation
# Each observation month is approximated as 21 trading days
out_dates_lists = np.linspace(3, 18, 16)
out_dates_lists = out_dates_lists * 21

# Define knock-out barrier levels (as percentages of initial price)
# The barrier is gradually decreasing over time (step-down structure)
P = np.linspace(1, 0.925, 16)

# Combine observation schedule and KO barriers
ko_p_list = pd.DataFrame({
    'out_dates_lists': out_dates_lists,
    'P': P
})

# ============================================================
# Historical Volatility Estimation of the Underlying Index
# ============================================================
# Estimate historical volatility of CSI 500 index, which is
# used as an input parameter for Monte Carlo simulation.

df = get_price(
    '000905.XSHG',
    start_date='2021-12-07',
    end_date='2022-12-07',
    frequency='daily',
    fields=None,
    skip_paused=False,
    fq='none'
)

# Compute daily log returns
daily_close = df['close']
daily_log_return = np.log(daily_close.pct_change() + 1)
daily_log_return.fillna(0, inplace=True)

# Annualize log returns assuming 252 trading days
year_pct_change = daily_log_return * np.sqrt(252)

# Rolling volatility estimation (100-day window)
vol = year_pct_change.rolling(window=100).std()

# ============================================================
# Futures Discount / Basis Adjustment
# ============================================================
# Estimate the annualized futures discount rate, which is
# incorporated as a dividend yield or carry cost in the
# risk-neutral pricing framework.

discount_mean = (
    IC_discount['dis_r_2'].mean() +
    IC_discount['dis_r_3'].mean()
) / 2

# Annualized discount rate used in simulation
D = discount_mean

# ============================================================
# Monte Carlo Simulation of Underlying Price Paths
# ============================================================
# Simulate price paths of the underlying index under a
# risk-neutral measure with drift adjustment for discount
# rate and volatility.

def simulation(S_0, r, D, sig, T, Nsteps, I):
    """
    Parameters
    ----------
    S_0 : float
        Initial level of the underlying index
    r : float
        Risk-free interest rate
    D : float
        Annualized discount rate (cost of carry)
    sig : float
        Volatility of the underlying
    T : float
        Product maturity (in years)
    Nsteps : int
        Number of time steps
    I : int
        Number of Monte Carlo simulation paths
    """

    # Time increment
    dt = float(T) / Nsteps

    # Initialize price path matrix
    S_path = np.zeros((Nsteps + 1, I))
    S_path[0] = S_0

    # Simulate GBM paths with capped daily movement
    for t in range(1, Nsteps + 1):
        z = np.random.standard_normal(I)

        S = S_path[t - 1] * np.exp(
            ((r - D) - 0.5 * sig ** 2) * dt +
            sig * np.sqrt(dt) * z
        )

        # Apply daily price limit (e.g., ±10%)
        S_cap = S_path[t - 1] * 1.1
        S_floor = S_path[t - 1] * 0.9

        temp = np.where(S > S_cap, S_cap, S)
        temp = np.where(S_floor > S, S_floor, temp)

        S_path[t, :] = temp

    # Plot simulated price paths
    plt.plot(S_path[:, :])
    plt.title('Simulated Underlying Price Paths')
    plt.xlabel('Time Steps')
    plt.ylabel('Underlying Price')
    plt.show()

# ============================================================
# Historical Path and Knock-Out Visualization
# ============================================================
# Visualize historical underlying price paths together with
# knock-out barriers and observation points.

df.columns = ['Tradingdate', 'open', 'Price', 'high', 'low', 'volume', 'money']
df = df[['Tradingdate', 'Price']]

# Define actual observation dates
df1 = pd.date_range(start='2023-03-07', end='2024-06-07', freq='D')
specific_dates = [
    '2023-03-07','2023-04-07','2023-05-08','2023-06-07',
    '2023-07-07','2023-08-07','2023-09-07','2023-10-09',
    '2023-11-07','2023-12-07','2024-01-08','2024-02-07',
    '2024-03-07','2024-04-08','2024-05-07','2024-06-07'
]

# Define KO barrier levels in price terms
P = np.linspace(1, 0.925, 16)
P = P * S_0

ko_p_list = pd.DataFrame({
    'out_dates_lists': specific_dates,
    'P': P
})

ko_p_list['out_dates_lists'] = ko_p_list['out_dates_lists'].apply(
    lambda x: datetime.strptime(x, '%Y-%m-%d').date()
)

# Plot underlying price, knock-in barrier, and KO levels
plt.plot(df['Tradingdate'], df['Price'])
plt.axhline(y=S_0 * 0.7, color='brown', linestyle='-.')
plt.scatter(ko_p_list['out_dates_lists'], ko_p_list['P'], color='r')

plt.legend(
    ['Underlying Index', 'Knock-in Barrier', 'Knock-out Level'],
    loc='upper right',
    fontsize=15
)
