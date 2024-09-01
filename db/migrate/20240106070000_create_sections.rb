class CreateSections < ActiveRecord::Migration[7.0]
  def change
    create_table :sections, id: :uuid do |t|
      t.string :name, null: false
      t.integer :seq, null: false
      t.uuid :note_id, null: false

      t.timestamps
    end

    add_index :sections, %i[seq note_id], unique: true
  end
end
