class CarSerializer < ActiveModel::Serializer
  attributes :id,
             :name,
             :maker,
             :model,
             :model_year,
             :license_plate,
             :tank_capacity
end
