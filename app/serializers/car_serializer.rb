class CarSerializer < ActiveModel::Serializer
  attributes :id, :name, :make, :model, :model_year, :license_plate, :tank_capacity
end
