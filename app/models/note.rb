class Note < ApplicationRecord
  # バリデーション
  validates :title, presence: true
  validates :uid, presence: true
  validates :seq, presence: true
end
