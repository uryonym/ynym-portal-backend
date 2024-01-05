class Section < ApplicationRecord
  # バリデーション
  validates :name, presence: true
  validates :uid, presence: true
  validates :seq, presence: true
  validates :note_id, presence: true
end
