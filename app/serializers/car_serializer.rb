# frozen_string_literal: true

class CarSerializer < ActiveModel::Serializer
  attributes :id,
    :name,
    :seq,
    :maker,
    :model,
    :model_year,
    :license_plate,
    :tank_capacity,
    :created_at,
    :updated_at
end
