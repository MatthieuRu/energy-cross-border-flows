create schema dexter;
CREATE TABLE dexter.energy_cross_border_flows (
  country_code_to varchar(2) not null,
  country_code_from varchar(2) not null,
  flow_timestamp timestamptz not null,
  capacity_mw integer not null,
  created_at date not null DEFAULT CURRENT_TIMESTAMP
);
SET timezone = 'Europe/Amsterdam';
create unique index "ci_flow_id_idx" on dexter.energy_cross_border_flows(country_code_to, country_code_from,flow_timestamp);