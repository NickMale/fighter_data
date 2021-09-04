CREATE TABLE "fighters" (
  "fighter_id" SERIAL PRIMARY KEY,
  "fighter_first" varchar NOT NULL,
  "fighter_last" varchar NOT NULL,
  UNIQUE("fighter_first", "fighter_last")
);

CREATE TABLE "weightclasses" (
  "weightclass_id" int PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "outcomes" (
  "outcome_id" int PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "bouts" (
  "bout_id" int PRIMARY KEY,
  "winner_id" int,
  "loser_id" int,
  "weightclass_id" int,
  "outcome_id" int
);

ALTER TABLE "bouts" ADD FOREIGN KEY ("winner_id") REFERENCES "fighters" ("fighter_id");

ALTER TABLE "bouts" ADD FOREIGN KEY ("loser_id") REFERENCES "fighters" ("fighter_id");

ALTER TABLE "bouts" ADD FOREIGN KEY ("weightclass_id") REFERENCES "weightclasses" ("weightclass_id");

ALTER TABLE "bouts" ADD FOREIGN KEY ("outcome_id") REFERENCES "outcomes" ("outcome_id");
