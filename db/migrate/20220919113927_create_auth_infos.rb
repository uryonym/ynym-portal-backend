class CreateAuthInfos < ActiveRecord::Migration[7.0]
  def change
    create_table :auth_infos, id: :uuid do |t|
      t.string :service_name, null: false 
      t.string :login_id, null: false
      t.string :password
      t.string :other

      t.timestamps
    end

    add_index :auth_infos, :service_name, unique: true
  end
end
