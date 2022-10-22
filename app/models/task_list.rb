class TaskList < ApplicationRecord
  # バリデーション
  validates :name, presence: true
  validates :uid, presence: true

  # アソシエーション
  belongs_to :user, primary_key: :uid, foreign_key: :uid
  belongs_to :share_user, class_name: 'User', primary_key: :share_uid, foreign_key: :uid, optional: true
  has_many :tasks, -> { order 'dead_line, created_at'}
end
