class CreateCars < ActiveRecord::Migration[7.0]
  def change
    create_table :cars, id: :uuid do |t|
      t.string :name, null: false
      t.integer :seq, null: false
      t.string :maker, null: false
      t.string :model, null: false
      t.integer :model_year, null: false
      t.string :license_plate
      t.integer :tank_capacity
      t.string :uid, null: false

      t.timestamps
    end

    add_index :cars, %i[seq uid], unique: true
  end
end
