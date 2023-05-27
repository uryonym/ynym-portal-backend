class Car < ApplicationRecord
  # バリデーション
  validates :name, presence: true
  validates :maker, presence: true
  validates :model, presence: true
  validates :model_year, presence: true

  # アソシエーション
  has_many :refuelings
end
