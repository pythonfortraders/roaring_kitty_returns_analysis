# Code for the video [How to Trade $GME like a Quant with Python](https://youtu.be/J5KYylYgGQ4?feature=shared)

When RoaringKitty tweets, the market listens. We collect a dataset of RoaringKitty tweets using Selenium to extract their timestamps from the browser, then we collect historical $GME price data to assess the market impact of these tweets. With historical prices, we calculate the forward returns for different time periods and plot a histogram to see how much predictive power a new tweet really has.
