class CreateNotes < ActiveRecord::Migration[7.0]
  def change
    create_table :notes, id: :uuid do |t|
      t.string :title, null: false
      t.string :content, null: false

      t.timestamps
    end
  end
end
