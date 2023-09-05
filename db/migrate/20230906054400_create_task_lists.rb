class CreateTaskLists < ActiveRecord::Migration[7.0]
  def change
    create_table :task_lists, id: :uuid do |t|
      t.string :name, null: false
      t.string :uid, null: false
      t.integer :seq, null: false

      t.timestamps
    end

    add_index :task_lists, [:uid, :seq], unique: true
  end
end
