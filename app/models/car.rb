# frozen_string_literal: true

class Car < ApplicationRecord
  # バリデーション
  validates :name, presence: true
  validates :seq, presence: true
  validates :maker, presence: true
  validates :model, presence: true
  validates :model_year, presence: true
  validates :license_plate, presence: true
  validates :tank_capacity, presence: true

  # アソシエーション
  belongs_to :user, primary_key: :uid, foreign_key: :uid
  has_many :refuelings, -> { order(refuel_datetime: :desc) }
end
