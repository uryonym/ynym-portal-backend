# frozen_string_literal: true

class Refueling < ApplicationRecord
  # バリデーション
  validates :refuel_datetime, presence: true
  validates :odometer, presence: true
  validates :fuel_type, presence: true
  validates :price, presence: true
  validates :total_cost, presence: true
  validates :is_full, presence: true
  validates :gas_stand, presence: true

  # アソシエーション
  belongs_to :user, primary_key: :uid, foreign_key: :uid
  belongs_to :car
end
