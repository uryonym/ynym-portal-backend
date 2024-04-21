class Task < ApplicationRecord
  # バリデーション
  validates :title, presence: true

  # アソシエーション
  belongs_to :user, primary_key: :uid, foreign_key: :uid
  belongs_to :task_list
end
