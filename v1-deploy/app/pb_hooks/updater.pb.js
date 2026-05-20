/// <reference path="../pb_data/types.d.ts" />

cronAdd("fill_aapl_gaps", "*/30 * * * *", () => {
    const collectionName = "data_nasdaq_aapl";
    const collection = $app.findCollectionByNameOrId(collectionName);

    // 1. Get the newest record
    let latestRecord;
    try {
        latestRecord = $app.findRecordsByFilter(collectionName, "", "-date", 1)[0];
    } catch (e) {
        latestRecord = null;
    }

    let nextSearchStart;
    if (latestRecord) {
        // Get the string from PB, parse it, and add 1 day (86400000 ms)
        const lastDate = new Date(latestRecord.getDateTime("date").string().replace(' ', 'T')); 
        nextSearchStart = new Date(lastDate.getTime() + 24 * 60 * 60 * 1000);
    } else {
        // Fallback if table is empty
        nextSearchStart = new Date("2022-12-13T00:00:00Z");
    }

    nextSearchStart.setUTCHours(0, 0, 0, 0);
    const p1 = Math.floor(nextSearchStart.getTime() / 1000);
    // Request a 7-day window to ensure we catch the next available trading day
    const p2 = p1 + (7 * 24 * 60 * 60); 

    console.log(`Checking for data after: ${nextSearchStart.toISOString().split('T')[0]}`);

    const url = `https://query1.finance.yahoo.com/v8/finance/chart/AAPL?period1=${p1}&period2=${p2}&interval=1d`;

    try {
        const response = $http.send({
            url: url,
            method: "GET",
            headers: { "User-Agent": "Mozilla/5.0" }
        });

        const data = response.json;
        const result = data.chart.result ? data.chart.result[0] : null;

        if (!result || !result.timestamp || result.timestamp.length === 0) {
            console.log("No data found in this range. (Market closed or date is in the future)");
            return;
        }

        const timestamps = result.timestamp;
        const quotes = result.indicators.quote[0];

        // Loop through the results to find the first valid (non-null) trading day
        let foundIndex = -1;
        for (let i = 0; i < timestamps.length; i++) {
            // Check if OHLC data exists for this timestamp
            if (quotes.open[i] !== null && quotes.close[i] !== null) {
                foundIndex = i;
                break;
            }
        }

        if (foundIndex === -1) {
            console.log("Found timestamps, but all OHLC data was null.");
            return;
        }

        const targetDate = new Date(timestamps[foundIndex] * 1000);
        const targetDateStr = targetDate.toISOString().split('T')[0];

        // Final check: Don't insert if this date is already the one we just had
        // (Prevents infinite loops if the API returns the 'last' day instead of 'next')
        if (latestRecord && targetDateStr === latestRecord.getDateTime("date").string().split(' ')[0]) {
            console.log("API returned the same date we already have. Waiting for market open.");
            return;
        }

        const record = new Record(collection);
        record.set("date", targetDateStr + " 00:00:00.000Z");
        record.set("open", quotes.open[foundIndex]);
        record.set("high", quotes.high[foundIndex]);
        record.set("low", quotes.low[foundIndex]);
        record.set("close", quotes.close[foundIndex]);
        record.set("volume", quotes.volume[foundIndex]);

        $app.save(record);
        console.log(`SUCCESS: Written date ${targetDateStr} to DB.`);

    } catch (err) {
        console.log("CRITICAL ERROR: " + err);
    }
});
