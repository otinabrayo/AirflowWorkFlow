INSERT INTO exchange_rate_hist
SELECT
    t.$1:time_last_update_utc::TIMESTAMP_NTZ AS timestamp,
    t.$1:base_code::VARCHAR AS base_currency,
    f.key::VARCHAR AS exchange_currency,
    f.value::FLOAT AS exchange_rate
FROM @my_s3_stage/oms/xrate_.json (FILE_FORMAT => 'my_json_format') t,
    LATERAL FLATTEN(input => t.$1:conversion_rates) f;