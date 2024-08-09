# frozen_string_literal: true

class RefuelingSerializer < ActiveModel::Serializer
  attributes :id,
    :refuel_datetime,
    :odometer,
    :fuel_type,
    :price,
    :total_cost,
    :is_full,
    :gas_stand,
    :created_at,
    :updated_at
end
