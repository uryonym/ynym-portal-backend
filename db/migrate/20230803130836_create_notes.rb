class CreateNotes < ActiveRecord::Migration[7.0]
  def change
    create_table :notes, id: :uuid do |t|
      t.string :name, null: false
      t.integer :seq, null: false
      t.string :uid, null: false

      t.timestamps
    end

    add_index :notes, %i[seq uid], unique: true
  end
end
