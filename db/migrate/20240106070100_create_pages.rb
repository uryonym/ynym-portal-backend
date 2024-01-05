class CreatePages < ActiveRecord::Migration[7.0]
  def change
    create_table :pages, id: :uuid do |t|
      t.string :title, null: false
      t.string :content, null: false
      t.string :uid, null: false
      t.integer :seq, null: false
      t.uuid :note_id, null: false
      t.uuid :section_id, null: false

      t.timestamps
    end

    add_index :pages, %i[section_id seq], unique: true
  end
end
