class Note < ApplicationRecord
  # バリデーション
  validates :title, presence: true
  validates :content, presence: true
end
