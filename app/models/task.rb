class Task < ApplicationRecord
  # バリデーション
  validates :title, presence: true
end
