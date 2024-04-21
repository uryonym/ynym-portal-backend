class CreateRefuelings < ActiveRecord::Migration[7.0]
  def change
    create_table :refuelings, id: :uuid do |t|
      t.datetime :refuel_datetime, null: false
      t.integer :odometer, null: false
      t.string :fuel_type, null: false
      t.integer :price, null: false
      t.integer :total_cost, null: false
      t.boolean :is_full, null: false, default: true
      t.string :gas_stand, null: false
      t.string :uid, null: false
      t.uuid :car_id, null: false

      t.timestamps
    end
  end
end
