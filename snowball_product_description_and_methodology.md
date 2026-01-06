# Snowball Product Description & Methodology

## 1. Product Overview

This project studies an enhanced step-down barrier Snowball structured product issued in December 2022, with the CSI 500 Index as the underlying asset. The product belongs to the class of yield-enhanced structured notes commonly issued in the Chinese structured products market.

Compared with standard Snowball products, this structure features a gradually decreasing knock-out barrier, which lowers the redemption threshold over time and increases the probability of early termination as maturity approaches.

---

## 2. Product Structure

The Snowball product incorporates the following key design features:

- **Step-down knock-out (KO) barrier**  
  The knock-out level decreases over time, allowing the product to be redeemed more easily in later observation periods.

- **Periodic observation dates**  
  The underlying index price is monitored on predefined monthly observation dates to determine whether early redemption is triggered.

- **Knock-in (KI) barrier**  
  The knock-in barrier is monitored continuously throughout the product life. Once breached, downside protection is removed.

- **Coupon-enhanced payoff**  
  Investors are compensated with an enhanced coupon in exchange for bearing tail risk.

---

## 3. Payoff Scenarios

The payoff structure can be decomposed into three mutually exclusive scenarios:

### 3.1 Early Knock-Out Scenario

If the underlying index price exceeds the knock-out barrier on any observation date, the product is redeemed early. The investor receives the principal plus accrued coupon proportional to the holding period.

### 3.2 No Knock-Out and No Knock-In Scenario

If the product survives to maturity without any knock-in or knock-out events, the investor receives the principal plus the full coupon.

### 3.3 Knock-In Without Knock-Out Scenario

If a knock-in event occurs at any time during the product life and no knock-out event is triggered, the final payoff becomes linked to the terminal performance of the underlying index, exposing the investor to downside risk.

This scenario-based decomposition highlights the asymmetric and negatively skewed payoff profile of Snowball products.

---

## 4. Pricing Methodology

### 4.1 Underlying Price Dynamics

The underlying index price is assumed to follow a geometric Brownian motion under the risk-neutral measure. The drift term is adjusted by incorporating a discount rate derived from index futures basis, which effectively acts as a dividend yield or cost-of-carry component.

### 4.2 Monte Carlo Simulation Framework

Monte Carlo simulation is used to generate a large number of underlying price paths from product inception to maturity. For each simulated path:

- Knock-in and knock-out conditions are continuously monitored
- Early redemption events are explicitly handled
- Cash flows are computed according to the product contract

The fair value of the Snowball product is obtained by averaging discounted payoffs across all simulated paths.

---

## 5. Parameter Selection

Key model parameters are calibrated using observable market data at the issuance date:

- **Initial price**: CSI 500 index level prior to issuance  
- **Risk-free rate**: Short-term SHIBOR rate  
- **Volatility**: Historical annualized volatility estimated using rolling windows  
- **Discount rate**: Average futures basis of CSI 500 index futures contracts  

This calibration ensures consistency between the pricing model and prevailing market conditions.

---

## 6. Risk Characteristics and Interpretation

Simulation results suggest that the Snowball product exhibits a high probability of early redemption and coupon payment, but also embeds significant downside risk in adverse market conditions. Losses tend to be infrequent but severe, leading to a negatively skewed payoff distribution.

The project demonstrates how Monte Carlo methods can be applied to evaluate complex structured products with strong path dependency and nonlinear payoffs.
