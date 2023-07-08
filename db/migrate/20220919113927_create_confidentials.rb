class CreateConfidentials < ActiveRecord::Migration[7.0]
  def change
    create_table :confidentials, id: :uuid do |t|
      t.string :service_name, null: false 
      t.string :login_id, null: false
      t.string :password
      t.string :other

      t.timestamps
    end
  end
end
