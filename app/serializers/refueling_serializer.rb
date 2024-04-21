class RefuelingSerializer < ActiveModel::Serializer
  attributes :id,
             :refuel_datetime,
             :odometer,
             :fuel_type,
             :price,
             :total_cost,
             :is_full,
             :gas_stand,
             :car_id
end
