from data_fetcher import get_commodity_data
from predictor import train_model, predict_next_close
from datetime import date, timedelta
from alert import alert

end = date.today()
start = end - timedelta(days=180)

df = get_commodity_data("GC=F", start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))

if df is not None and not df.empty:
    model, feature_df = train_model(df)
    predicted = predict_next_close(model, feature_df)
    current = float(feature_df["Close"].iloc[-1].item())

    print(f"📈 Current Price: ${current:.2f}")
    print(f"🤖 Predicted Next Close: ${predicted:.2f}")
    print(f"📊 Expected Change: {((predicted - current) / current) * 100:.2f}%")
    
    alert, signal, change = alert(current, predicted, threshold=0.015)  # 1.5% default
    if alert:
        print(f"🚨 ALERT: {signal} SIGNAL — Expected change: {change:.2f}%")
    else:
        print(f"✅ No alert. Market stable. Change only: {change:.2f}%")

else:
    print("Data fetch failed or returned no data.")
