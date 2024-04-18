class TaskList < ApplicationRecord
  # バリデーション
  validates :name, presence: true
  validates :seq, presence: true
  validates :uid, presence: true

  # アソシエーション
  belongs_to :user, primary_key: :uid, foreign_key: :uid
  has_many :tasks, -> { order :dead_line, :created_at }
end
