/*
  # Create watchlist table

  1. New Tables
    - `watchlist`
      - `id` (uuid, primary key)
      - `user_id` (uuid, foreign key to users.id)
      - `title` (text, not null)
      - `image_url` (text, not null)
      - `category` (text, not null, check constraint for valid categories)
      - `created_at` (timestamptz, default now())

  2. Security
    - Enable RLS on `watchlist` table
    - Add policy for users to read their own watchlist items
    - Add policy for users to insert their own watchlist items
    - Add policy for users to update their own watchlist items
    - Add policy for users to delete their own watchlist items

  3. Constraints
    - Foreign key constraint on user_id
    - Check constraint for valid categories (Movie, Anime, Series)
*/

CREATE TABLE IF NOT EXISTS watchlist (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title text NOT NULL,
  image_url text NOT NULL,
  category text NOT NULL CHECK (category IN ('Movie', 'Anime', 'Series')),
  created_at timestamptz DEFAULT now()
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_watchlist_user_id ON watchlist(user_id);
CREATE INDEX IF NOT EXISTS idx_watchlist_category ON watchlist(category);
CREATE INDEX IF NOT EXISTS idx_watchlist_created_at ON watchlist(created_at DESC);

ALTER TABLE watchlist ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own watchlist items"
  ON watchlist
  FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own watchlist items"
  ON watchlist
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own watchlist items"
  ON watchlist
  FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own watchlist items"
  ON watchlist
  FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);