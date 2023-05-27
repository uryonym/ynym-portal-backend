class Refueling < ApplicationRecord
  # バリデーション
  validates :refuel_datetime, presence: true
  validates :odometer, presence: true
  validates :fuel_type, presence: true
  validates :price, presence: true
  validates :quantity, presence: true
  validates :full_flag, presence: true
  validates :gas_stand, presence: true

  # アソシエーション
  belongs_to :car
end
