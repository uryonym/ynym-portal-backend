class RefuelingSerializer < ActiveModel::Serializer
  attributes :id, :refuel_datetime, :odometer, :fuel_type, :price, :total_cost, :full_flag, :gas_stand, :car_id
end
