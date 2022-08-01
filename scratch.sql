UPDATE test_data.ticker_state s 
SET feed_record_count = (SELECT COUNT(1) FROM test_data.market_feed WHERE symbol = 'NET')
WHERE symbol = 'NET';
UPDATE test_data.ticker_state s 
SET feed_record_count = (SELECT COUNT(1) FROM test_data.market_feed WHERE symbol = 'DOCN')
WHERE symbol = 'DOCN';


