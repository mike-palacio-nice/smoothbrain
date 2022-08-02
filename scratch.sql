UPDATE test_data.economic_feed s 
SET treasury_yield_10_yr = foo.lag_ty
FROM (SELECT metric_ts, LAG(treasury_yield_10_yr, 1) OVER (ORDER BY metric_ts) lag_ty FROM test_data.economic_feed) foo
WHERE treasury_yield_10_yr IS NULL
AND foo.metric_ts = s.metric_ts;



