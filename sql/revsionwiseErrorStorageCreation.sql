create table revisionwise_error_store
(
id NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY,
date_key date,
entity_tag varchar2(100),
revision_no varchar2(3CHAR),
mae number,
mape number,
rmse number,
rmse_percentage number,
constraints unique_mw_error unique(date_key,entity_tag,revision_no),
constraints pk_mw_error primary key(id)
)