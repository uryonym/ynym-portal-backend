class Note < ApplicationRecord
  # バリデーション
  validates :name, presence: true
  validates :uid, presence: true
  validates :seq, presence: true
end
