class Task < ApplicationRecord
  # バリデーション
  validates :title, presence: true

  # アソシエーション
  belongs_to :task_list
end
